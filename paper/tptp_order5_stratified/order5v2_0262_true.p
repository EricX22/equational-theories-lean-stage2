% order5v2_0262  eq1=6796 eq2=291  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(X,f(f(Z,W),f(W,U)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Z),X),Y) )).
