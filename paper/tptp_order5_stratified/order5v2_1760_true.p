% order5v2_1760  eq1=51852 eq2=45557  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(f(Z,Z),f(Y,X)),X) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(f(X,X),W),W)) )).
