% hard3_0013  eq1=58 eq2=3050  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(Y,f(Z,X))) )).
fof(goal, conjecture, ! [X] : ( X = f(f(f(f(X,X),X),X),X) )).
