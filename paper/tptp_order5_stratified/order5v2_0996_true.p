% order5v2_0996  eq1=9835 eq2=36299  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(X,f(W,U)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(f(X,X),Y),f(Y,Z)),Y) )).
