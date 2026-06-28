% hard3_0189  eq1=1681 eq2=2203  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(Y,X),f(f(X,X),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Z),Z),f(Z,X)) )).
