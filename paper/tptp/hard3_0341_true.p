% hard3_0341  eq1=3247 eq2=2389  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),U),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(Z,f(Y,Z))),X) )).
