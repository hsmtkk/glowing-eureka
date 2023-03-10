import { Construct } from "constructs";
import { App, TerraformStack } from "cdktf";
import * as google from '@cdktf/provider-google';

const project = 'glowing-eureka';
const repository = 'glowing-eureka';
const region = 'us-central1';

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    new google.provider.GoogleProvider(this, 'google', {
      project,
    });

    new google.artifactRegistryRepository.ArtifactRegistryRepository(this, 'registry', {
      format: 'docker',
      location: region,
      repositoryId: 'registry',
    });

    new google.cloudbuildTrigger.CloudbuildTrigger(this, 'trigger', {
      filename: 'cloudbuild.yaml',
      github: {
        owner: 'hsmtkk',
        name: repository,
        push: {
          branch: 'main',
        },
      },
    });

    const exampleService = new google.cloudRunV2Service.CloudRunV2Service(this, 'example', {
      location: region,
      name: 'example',
      template: {
        containers: [{
          env: [{
            name: 'DEBUG',
            value: 'true',
          }],
          image: 'us-central1-docker.pkg.dev/glowing-eureka/registry/app:latest',
        }],
      },
    });

    const publicData = new google.dataGoogleIamPolicy.DataGoogleIamPolicy(this, 'publicData', {
      binding: [{
        role: 'roles/run.invoker',
        members: ['allUsers'],
      }],
    });

    new google.cloudRunServiceIamPolicy.CloudRunServiceIamPolicy(this, 'publicPolicy', {
      location: region,
      policyData: publicData.policyData,
      project,
      service: exampleService.name,
    });

  }
}

const app = new App();
new MyStack(app, "glowing-eureka");
app.synth();
