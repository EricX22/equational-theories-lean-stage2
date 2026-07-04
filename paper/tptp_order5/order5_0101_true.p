% order5_0101  eq1=28912 eq2=62535  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),X),Y),f(W,U)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(f(X,Y),Z) = f(f(f(W,W),U),Y) )).
