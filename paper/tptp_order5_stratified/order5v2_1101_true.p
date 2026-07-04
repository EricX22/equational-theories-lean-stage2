% order5v2_1101  eq1=11233 eq2=62056  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Y,f(Y,X)),f(Z,Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(f(X,Y),Y) = f(f(f(X,X),X),Z) )).
