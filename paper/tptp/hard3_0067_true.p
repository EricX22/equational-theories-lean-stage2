% hard3_0067  eq1=453 eq2=615  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(X,f(Y,f(Z,f(Y,W)))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(X,f(f(X,X),Y))) )).
