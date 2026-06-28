% hard3_0094  eq1=723 eq2=3089  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Y,f(f(Z,X),X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(f(X,Y),Z),Y),X) )).
