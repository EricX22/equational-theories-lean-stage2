% hard3_0029  eq1=138 eq2=4183  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Z,Y),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(f(Y,Z),Z),Y) )).
