% hard3_0156  eq1=1318 eq2=2078  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,X),Z),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,Y),Z),f(Z,X)) )).
