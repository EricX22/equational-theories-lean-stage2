% order5_0179  eq1=34409 eq2=51858  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,f(Y,Z))),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(f(Z,Z),f(Y,Y)),Z) )).
